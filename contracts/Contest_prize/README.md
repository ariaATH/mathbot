# ContestPrize

قرارداد هوشمند مسابقه‌های MathBot: هزینه ثبت‌نام و بودجه جایزه هر مسابقه را نگه می‌دارد و جوایز را به برندگان می‌فرستد.
شناسه هر مسابقه روی قرارداد **همان `id` رکورد `Contest` در دیتابیس جنگو** است.

مستند کامل اتصال به بک‌اند و فرانت: [`docs/blockchain-integration.md`](../../docs/blockchain-integration.md)

## ساختار

```
src/ContestPrize.sol            قرارداد
test/ContestPrize.t.sol         تست‌های واحد + fuzz
test/ContestPrize.invariant.t.sol   تست invariant (حسابداری موجودی)
script/ContestPrize.s.sol       استقرار
script/export-abi.sh            ساخت ABI برای بک‌اند و فرانت
```

## Build و تست

```bash
forge build --sizes
forge test -vvv
forge coverage --no-match-coverage '\.t\.sol|\.s\.sol'
forge fmt            # CI با forge fmt --check چک می‌کند
```

وابستگی‌ها: `lib/forge-std` یک submodule است، پس بعد از clone:

```bash
git submodule update --init --recursive
```

## استقرار

```bash
cp .env.example .env     # SEPOLIA_RPC_URL و PRIVATE_KEY را پر کنید
forge script script/ContestPrize.s.sol:Deploycontestprize --rpc-url sepolia --broadcast --verify
```

- به جای `PRIVATE_KEY` می‌توانید از keystore رمزگذاری‌شده استفاده کنید:
  `cast wallet import deployer --interactive` و سپس `--account deployer`.
- اگر `CONTRACT_OWNER` ست شود، مالکیت بلافاصله بعد از استقرار به آن آدرس (کیف پول بک‌اند) منتقل می‌شود.

بعد از استقرار:

1. آدرس قرارداد را در `backend/.env` → `CONTEST_CONTRACT_ADDRESS` بگذارید.
2. اگر قرارداد تغییر کرده: `bash script/export-abi.sh` و کامیت خروجی‌ها.

## نکات قرارداد

- **مالک = کیف پول بک‌اند**. ساخت مسابقه، اعلام برندگان، لغو، بازپرداخت و برداشت فقط با مالک انجام می‌شود.
- پول هر مسابقه جداگانه حساب می‌شود؛ مجموع `Total_amount` مسابقه‌ها همیشه برابر موجودی قرارداد است
  (تست invariant همین را چک می‌کند).
- `signup(id, userRef)` علاوه بر پرداخت، شناسه کاربر بک‌اند را ذخیره می‌کند تا بک‌اند بتواند پرداخت را
  به همان کاربر نسبت دهد.
- ارسال مستقیم اتر به قرارداد رد می‌شود (تابع `receive` ندارد) تا پولی بدون ثبت‌نام گم نشود.
- `renounceOwnership` غیرفعال است (وگرنه پول مسابقه‌ها برای همیشه قفل می‌شد).
- در شرایط اضطراری `pause()` همه عملیات مالی را متوقف می‌کند.

نام توابع عمدا به همان شکل قبلی (`Addcomp`، `Awardwinners`، ...) نگه داشته شده تا بک‌اند و فرانت تغییر نکنند.
