# اتصال بلاکچین (ContestPrize)

لایه بلاکچین آماده و تست‌شده است. این سند فقط می‌گوید **تیم بک‌اند و فرانت چه کاری باید انجام دهند**.

- قرارداد: `contracts/Contest_prize/` · بک‌اند: `backend/contractapi/` · فرانت: `frontend/src/blockchain/`
- قرارداد فقط پول را نگه می‌دارد؛ منطق مسابقه در جنگو می‌ماند. **شناسه مسابقه روی قرارداد = `id` رکورد `Contest` در دیتابیس.**

## جریان کار

```
ادمین  → POST /api/contract/admin/contests/        → قرارداد: مسابقه ساخته می‌شود
کاربر  → متامسک: signup(contestId, userId) + پرداخت
       → POST /api/contests/<id>/signup/ {wallet_address, tx_hash}
         بک‌اند با verify_signup پرداخت را چک می‌کند → Participation ساخته می‌شود
ادمین  → POST .../award/top3/ (یا سایر حالت‌ها)     → جایزه به برندگان واریز می‌شود
```

کاربر هنگام پرداخت، `id` کاربری‌اش را هم داخل تراکنش می‌فرستد؛ قرارداد آن را ذخیره می‌کند تا بک‌اند مطمئن شود
این کیف پول واقعا برای همین کاربر پول داده (کسی نمی‌تواند تراکنش دیگری را به اسم خودش جا بزند).

## راه‌اندازی محلی

```bash
anvil                                           # شبکه تستی محلی (ترمینال جدا)
cd contracts/Contest_prize && forge build
PRIVATE_KEY=<anvil-key-0> forge script script/ContestPrize.s.sol:Deploycontestprize \
  --rpc-url http://127.0.0.1:8545 --broadcast    # آدرس قرارداد را چاپ می‌کند
```

آدرس را در `backend/.env` بگذارید (بقیه متغیرها در `backend/.env.example`):

```env
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
BLOCKCHAIN_CHAIN_ID=31337
CONTEST_CONTRACT_ADDRESS=0x...
BLOCKCHAIN_OWNER_PRIVATE_KEY=<anvil-key-0>
```

اگر این متغیرها خالی باشند، بقیه سایت عادی کار می‌کند و فقط APIهای بلاکچین `503` می‌دهند.

---

## تیم بک‌اند

**۱) مدل‌ها** (`contests/models.py`):

```python
class Contest(models.Model):
    price = models.DecimalField(max_digits=30, decimal_places=18, default=0)   # الان TextField است
    chain_tx_hash = models.CharField(max_length=66, blank=True, default='')

class Participation(models.Model):
    wallet_address = models.CharField(max_length=42, blank=True, default='')   # جایزه به همین آدرس می‌رود
    signup_tx_hash = models.CharField(max_length=66, blank=True, default='')
```

**۲) ثبت مسابقه روی قرارداد** بعد از ساخت در دیتابیس:

```python
from contractapi import services

tx = services.create_contest(
    contest.id, price_eth=contest.price, signup_deadline=contest.start_time, user=request.user
)
contest.chain_tx_hash = tx.tx_hash
```

**۳) تایید پرداخت در `ContestSignupAPIView`** (مهم‌ترین قسمت — قبل از ساخت `Participation`):

```python
from contractapi import services
from contractapi.errors import BlockchainError

wallet = (request.data.get('wallet_address') or '').strip()
tx_hash = request.data.get('tx_hash')
try:
    on_chain = services.get_contest(contest.id)          # None = روی قرارداد ثبت نشده
    if on_chain and not on_chain['is_free']:
        if not wallet or not services.verify_signup(contest.id, wallet, request.user.id, tx_hash=tx_hash):
            return Response({'error': 'payment_not_found', 'detail': 'پرداخت شما روی بلاکچین پیدا نشد.'}, status=400)
except BlockchainError as exc:
    return Response(exc.as_dict(), status=exc.http_status)

Participation.objects.create(contest=contest, user=request.user,
                             wallet_address=wallet, signup_tx_hash=tx_hash or '')
```

هرگز به ادعای فرانت درباره پرداخت اعتماد نکنید؛ `verify_signup` مستقیم از قرارداد می‌خواند.

**۴) بقیه توابع سرویس** (همه `ContractTransaction` برمی‌گردانند):

```python
services.cancel_contest(id, user=...)               services.refund_participants(id, wallets, user=...)
services.award_top3(id, a, b, c, user=...)          services.award_with_percentage(id, a, b, c, [50,30,10], user=...)
services.award_fixed(id, a, b, c, ['0.5','0.3','0.1'], user=...)
services.award_duel(id, winner, user=...)           services.award_custom(id, winners, amounts, user=...)
services.withdraw_owner_share(id, treasury, user=...)   # سهم سایت بعد از پایان
```

**۵) باگ‌های موجود در اپ `contests` که باید رفع شوند:**

- `ContestsCreateAPIView` بدون `serializer_class` است → `POST /api/contests/create/` همین حالا ۵۰۰ می‌دهد؛ ضمنا permission آن باید `IsAdminUser` شود (الان هر کاربری می‌تواند مسابقه بسازد).
- `ContestsDeleteAPIView` از `IsOwnerOrAdmin` استفاده می‌کند که `obj.creator` را چک می‌کند ولی فیلد مدل `created_by` است.
- پوشه `migrations/` در `.gitignore` است و کانتینر موقع بالا آمدن `makemigrations` می‌زند — برای پروداکشن خطرناک است.
- `DEBUG = True` و `ALLOWED_HOSTS = ["*"]` ثابت هستند؛ `CommonMiddleware` دوبار آمده و `CorsMiddleware` باید بالاتر از آن باشد.
- سرویس `backend` در `docker-compose.yml` هیچ `env_file` ندارد.

---

## تیم فرانت

`ethers` نصب شده و کل منطق در `src/blockchain/` است؛ فقط UI مانده. تنظیمات قرارداد خودکار از
`GET /api/contract/config/` خوانده می‌شود (نیازی به متغیر محیطی نیست).

**دکمه اتصال کیف پول:**

```jsx
import { useWallet, shortAddress } from '../blockchain';

const w = useWallet();
if (!w.hasWallet)        return <a href="https://metamask.io/download/">نصب متامسک</a>;
if (!w.address)          return <button onClick={w.connect}>{w.connecting ? '...' : 'اتصال کیف پول'}</button>;
if (!w.isCorrectNetwork) return <button onClick={w.switchNetwork}>تغییر شبکه به {w.expectedNetworkLabel}</button>;
return <span>{shortAddress(w.address)}</span>;
```

**ثبت‌نام در مسابقه:**

```jsx
import { signupForContest, toFriendlyError } from '../blockchain';
import config from '../utils/config.js';

try {
    setStep('کیف پول را تایید کنید');
    const { tx, wallet } = await signupForContest({ contestId: contest.id });

    setStep('در حال تایید تراکنش...');          // چند ثانیه طول می‌کشد
    await tx.wait();

    setStep('در حال ثبت نهایی...');
    await config().post(`/contests/${contest.id}/signup/`, { wallet_address: wallet, tx_hash: tx.hash });
} catch (err) {
    setError(toFriendlyError(err).message);      // پیام آماده فارسی
}
```

توابع دیگر: `claimRefund(contestId)` برای مسابقه لغو شده، `fetchContestFromBackend(contestId)` برای نمایش
وضعیت روی‌زنجیره‌ای بدون نیاز به کیف پول، `hasPaidForContest(contestId)`.

**نکات:**

- مبلغ را هیچ‌وقت از UI تعیین نکنید؛ `signupForContest` قیمت را از خود قرارداد می‌خواند.
- اگر کاربر وسط کار صفحه را ببندد، پول پرداخت شده ولی ثبت‌نام کامل نشده؛ با زدن دوباره دکمه، خطای
  `AlreadyRegistered` می‌گیرید و فقط کافی است درخواست بک‌اند را دوباره بفرستید.
- `screens/Contest.js` الان کاملا ثابت و تستی است و باید اطلاعات را از `/api/contests/<id>/` بگیرد.
- باگ موجود: `utils/api.js` از `process.env.SERVER_APP_API_URL` استفاده می‌کند، ولی CRA فقط متغیرهای
  `REACT_APP_` را داخل بیلد می‌گذارد → در پروداکشن همیشه `localhost:8000` می‌شود. به `REACT_APP_API_URL` تغییر دهید.

---

## API بک‌اند (زیر `/api/contract/`)

| متد | آدرس | دسترسی |
|---|---|---|
| GET | `config/` | عمومی |
| GET | `contests/<id>/` | عمومی — وضعیت مسابقه روی زنجیره |
| GET | `contests/<id>/participants/<wallet>/` | کاربر لاگین‌کرده |
| POST | `admin/contests/` | ادمین — `contest_id`, `price_eth`, `signup_deadline`, `budget_eth?` |
| POST | `admin/contests/<id>/{deadline,budget,cancel,refund,withdraw}/` | ادمین |
| POST | `admin/contests/<id>/award/{top3,percentage,fixed,duel,custom}/` | ادمین |
| POST | `admin/{pause,unpause}/` · GET `admin/owner/` | ادمین |
| GET | `admin/transactions/` و `admin/transactions/<tx_hash>/` | ادمین |

پاسخ `202` یعنی تراکنش **ارسال** شده (نه تایید‌شده): `{"tx_hash", "status": "pending", "explorer_url"}` —
وضعیت نهایی را از `admin/transactions/<tx_hash>/` بگیرید.
خطاها همیشه `{"error": "<کد>", "detail": "<پیام فارسی>"}` هستند؛ کد خطا در بک‌اند و فرانت یکسان است
(`ContestNotFound`، `SignupClosed`، `AlreadyRegistered`، `InsufficientContestBalance`، `EnforcedPause`، ...).
لیست کامل: `backend/contractapi/errors.py` و `frontend/src/blockchain/errors.js`.
مستندات تعاملی: `/swagger/` با کاربر ادمین.

---

## امنیت

- `BLOCKCHAIN_OWNER_PRIVATE_KEY` مالک قرارداد است و به همه پول‌ها دسترسی دارد: فقط در `.env` سرور، هرگز در گیت، و با موجودی کم (در حد کارمزد). سهم سایت را با `withdrawOwner` به کیف پول سرد منتقل کنید.
- APIهای مالی فقط برای `is_staff` باز هستند؛ همه تراکنش‌ها در جدول `ContractTransaction` لاگ می‌شوند.
- موجودی کیف پول سرور را چک کنید (`GET /api/contract/admin/owner/`)؛ خالی شدنش یعنی اعلام برندگان شکست می‌خورد.
- در شرایط اضطراری `pause()` همه‌چیز را متوقف می‌کند.
- تا قبل از بازبینی امنیتی مستقل، فقط روی تست‌نت (Sepolia).

## تست

```bash
cd contracts/Contest_prize && forge test                                   # ۵۰ تست قرارداد
cd backend && BLOCKCHAIN_TEST_RPC_URL=http://127.0.0.1:8545 python manage.py test contractapi
cd frontend && npm test -- --watchAll=false --testPathPattern blockchain   # با anvil، جزئیات بالای فایل تست
```

بعد از هر تغییر در `ContestPrize.sol`، حتما `bash script/export-abi.sh` را اجرا و خروجی را کامیت کنید
(CI اگر ABI قدیمی باشد خطا می‌دهد).
