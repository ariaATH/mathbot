# اتصال بلاکچین (ContestPrize)

لایه بلاکچین (قرارداد + کدهای اتصال) نوشته و تست شده است. این سند می‌گوید **تیم بک‌اند و فرانت چه کاری باید انجام دهند**.

- قرارداد: `contracts/Contest_prize/` · بک‌اند: `backend/contractapi/` · فرانت: `frontend/src/blockchain/`
- قرارداد فقط پول را نگه می‌دارد؛ منطق مسابقه در جنگو می‌ماند. **شناسه مسابقه روی قرارداد = `id` رکورد `Contest` در دیتابیس.**

| چه کسی | چه کاری |
|---|---|
| مسئول بک‌اند / سرور | **استقرار قرارداد و ساخت کیف پول سرور** (بخش «استقرار»)، تغییر مدل‌ها و تایید پرداخت |
| مسئول فرانت | رابط کاربری اتصال کیف پول و ثبت‌نام |

استقرار قرارداد عمدا به عهده مسئول سرور است، چون کلید خصوصی مالک قرارداد باید روی همان سروری بماند
که خودش مدیریتش می‌کند.

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

## استقرار روی تست‌نت (وظیفه مسئول بک‌اند / سرور)

> این کار باید با **کیف پول خودتان** انجام شود: کلید خصوصی مالک قرارداد روی سرور می‌ماند و به همه
> پول مسابقه‌ها دسترسی دارد، پس کسی که سرور دستش است باید آن را بسازد و نگه دارد.

**۱) یک کیف پول مخصوص سرور بسازید** — در متامسک یک اکانت **جدید** (نه کیف پول شخصی‌تان) بسازید و
کلید خصوصی‌اش را بردارید (Account details → Show private key).

**۲) اتر تستی بگیرید:** شبکه را روی Sepolia بگذارید و از یک faucet (مثلا `sepoliafaucet.com` یا
faucet گوگل‌کلاد) حدود ۰.۵ اتر تستی به آدرس این کیف پول بگیرید — هم برای کارمزد، هم برای بودجه
جایزه مسابقه‌های رایگان.

**۳) یک RPC بگیرید:** در Infura یا Alchemy یک پروژه رایگان بسازید و آدرس Sepolia آن را بردارید.

**۴) فایل env قرارداد:**

```bash
cd contracts/Contest_prize
cp .env.example .env      # SEPOLIA_RPC_URL و PRIVATE_KEY (کلید کیف پول سرور) را پر کنید
```

امن‌تر (اختیاری): به جای نوشتن کلید در فایل، `cast wallet import deployer --interactive` بزنید و در
دستور بعدی `--account deployer` اضافه کنید.

**۵) استقرار:**

```bash
forge build
forge script script/ContestPrize.s.sol:Deploycontestprize --rpc-url sepolia --broadcast --verify
```

خروجی `ContestPrize deployed at: 0x...` را بردارید. (`--verify` به `ETHERSCAN_API_KEY` نیاز دارد؛
بدون آن هم استقرار انجام می‌شود، فقط سورس روی اکسپلورر نمایش داده نمی‌شود.)
اگر خواستید با کیف پول دیگری deploy کنید ولی مالکیت دست کیف پول سرور باشد، قبلش در `.env` مقدار
`CONTRACT_OWNER=<آدرس کیف پول سرور>` را بگذارید.

**۶) بک‌اند را تنظیم کنید** (`backend/.env`) و سرور را ری‌استارت کنید:

```env
BLOCKCHAIN_RPC_URL=<همان RPC مرحله ۳>
BLOCKCHAIN_CHAIN_ID=11155111
CONTEST_CONTRACT_ADDRESS=<آدرس مرحله ۵>
BLOCKCHAIN_OWNER_PRIVATE_KEY=<کلید کیف پول سرور>
BLOCKCHAIN_EXPLORER_URL=https://sepolia.etherscan.io
```

**۷) تست دود:**

```bash
curl -H "Authorization: Bearer <admin-jwt>" http://localhost:8000/api/contract/admin/owner/
# باید server_wallet_is_owner: true و موجودی غیرصفر برگرداند
```

بعد یک مسابقه آزمایشی بسازید، با یک کیف پول دیگر ثبت‌نام کنید، جایزه بدهید و سهم سایت را برداشت کنید.

**نکات نگهداری:**

- کلید خصوصی فقط در `.env` سرور بماند — نه در گیت، نه در تلگرام، نه در اسکرین‌شات. اگر لو رفت:
  `POST /api/contract/admin/pause/`، بعد با `withdrawOwner` پول‌ها را خارج کنید و قرارداد را با کیف
  پول جدید دوباره deploy کنید.
- موجودی کیف پول سرور را کم نگه دارید و سهم سایت را دوره‌ای به یک کیف پول سرد منتقل کنید.
- هر deploy دوباره یعنی آدرس جدید؛ مسابقه‌های قبلی روی قرارداد قدیمی می‌مانند، پس قبل از تعویض،
  جوایز و برداشت‌های قرارداد قبلی را تسویه کنید.
- برای شبکه اصلی (mainnet) اول یک بازبینی امنیتی مستقل لازم است.

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

- APIهای مالی فقط برای `is_staff` باز هستند؛ همه تراکنش‌ها در جدول `ContractTransaction` لاگ می‌شوند و در پنل ادمین دیده می‌شوند.
- موجودی کیف پول سرور را مرتب چک کنید (`GET /api/contract/admin/owner/`)؛ خالی شدنش یعنی اعلام برندگان شکست می‌خورد.
- در شرایط اضطراری `POST /api/contract/admin/pause/` همه عملیات مالی را متوقف می‌کند.
- بقیه نکات مربوط به کلید و کیف پول در بخش «استقرار» آمده است.

## تست

```bash
cd contracts/Contest_prize && forge test                                   # ۵۰ تست قرارداد
cd backend && BLOCKCHAIN_TEST_RPC_URL=http://127.0.0.1:8545 python manage.py test contractapi
cd frontend && npm test -- --watchAll=false --testPathPattern blockchain   # با anvil، جزئیات بالای فایل تست
```

بعد از هر تغییر در `ContestPrize.sol`، حتما `bash script/export-abi.sh` را اجرا و خروجی را کامیت کنید
(CI اگر ABI قدیمی باشد خطا می‌دهد).
