# How to use with planorama - a24 edition

1. Install the dependencies into a venv - they are in requirements.txt
2. Install conguide in the venv with `python setup.py install` in the main folder
3. use the `plano_connector.py` script to generate a file called plano-arisia.jsonp
4. run `conguide -c conguide/arisia.cfg all` to run the conguide commands for a24
5. send the `Bios`, `Schedule`, `Grid`, and `Tracks` files to `webmaster@arisia.org`
