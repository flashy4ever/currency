# currency

CLI currency converter

## Usage

### Commands

#### positional arguments

input&emsp;&emsp;input in format of "100 eur to usd"

#### options

-h, --help&emsp;&emsp;show help message<br>
-l, --list&emsp;&emsp;return list of available currencies

### Windows

1. Go to [this](https://exchangerate-api.com/) website and get your api key

2. Set the environment variable:

```powershell
$ setx CURRENCY_API_KEY "your key"
```

System restart may be needed after this operation

3. Download [latest github release](https://github.com/flashy4ever/currency/releases/latest)

4. Run program in terminal

```powershell
$ ./currency "49.99 gbp to rub"
> 49.99 GBP to RUB = 5362.63 RUB
```

### Other

1. Go to [this](https://exchangerate-api.com/) website and get your api key

2. Set the environment variable:

```bash
$ export CURRENCY_API_KEY "your key"
```

System restart may be needed after this operation

3. Clone the repository

```bash
$ git clone https://github.com/flashy4ever/currency.git
$ cd currency
```

4. Run program in terminal

```bash
$ py currency.py " " --list
> All available currencies:
> AED: UAE Dirham
> AFN: Afghan Afghani
> ...
```
