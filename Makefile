all:
	@echo "Installing the requirements"
	@python3 -m pip3 install -r requirements.txt

init:
	@echo "Creating output folders..."
	@mkdir -p "out"
	@mkdir -p "out/usages"
	@mkdir -p "out/cookies"
	@mkdir -p "out/plots"
	@cp assets/_empty.config.toml config.toml

install:
	@echo "Installing the requirements"
	@python3 -m pip3 install -r requirements.txt

clean:
	@echo "Cleaning output folders..."
	@rm -rf out/usages/*.csv
	@rm -rf out/plots/*.png
	@rm -rf out/cookies/*.pkl