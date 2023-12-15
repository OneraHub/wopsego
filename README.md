# wopsego
**Legacy Python 2.7** WhatsOpt API for SEGOMOE Onera Optimizer.
If you have Python 3, please refer to SEGOMOE as WhatsOpt web service
* [single-objective optimization](https://github.com/whatsopt/WhatsOpt-Doc/blob/master/whatsopt_segomoe.ipynb)
* [multi-objective optimization](https://github.com/whatsopt/WhatsOpt-Doc/blob/master/whatsopt_segmoomoe.ipynb)


## Prerequesite

You need an account on the [WhatsOpt server](https://ether.onera.fr). See [contact](https://github.com/whatsopt/WhatsOpt-Doc#contact).

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



