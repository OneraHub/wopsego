# wopsego
WhatsOpt API for SEGOMOE Onera Optimizer

## Prerequesite

You need an account on the [WhatsOpt server](https://ether.onera.fr). See [contact](https://github.com/OneraHub/WhatsOpt-Doc#contact).

You have to be logged in WhatsOpt server before using WhatsOpt SEGOMOE API.
Run the following command:

```bash
wop login https://ether.onera.fr/whatsopt
```

## Install

```bash
git clone https://github.com/OneraHub/wopsego
cd wopsego
pip install -e .
```

## Examples

```bash
python examples/unconstrained_optim.py
```
or

```bash
python examples/constrained_optim.py
```



