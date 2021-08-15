# ************************************************#
#                                                 #
#    Makefile                                     #
#                                                 #
#    Aids in building and distributing package    #
#                                                 #
# ************************************************#

# Variables
PKG_NAME      = webexteamssdk
PYTHON        = python3

RELATED_PKGS = webexteamssdk
DEPENDENCIES = future requests>=2.4.2 requests-toolbelt PyJWT

help:
	@echo "develop				Installs package into development mode"
	@echo "undevelop			Uninstalls package"

develop:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Building and installing $(PKG_NAME) development distributable: $@"
	@echo ""

	@pip uninstall -y $(RELATED_PKGS) || true
	@pip install $(DEPENDENCIES)

	@$(PYTHON) setup.py develop --no-deps

	@echo ""
	@echo "Completed building and installing: $@"
	@echo ""
	@echo "Done."
	@echo ""


undevelop:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Uninstalling $(PKG_NAME) development distributable: $@"
	@echo ""

	@$(PYTHON) setup.py develop --no-deps -q --uninstall

	@echo ""
	@echo "Completed uninstalling: $@"
	@echo ""
	@echo "Done."
	@echo ""