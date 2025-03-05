.PHONY: build deploy all

build:
	ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/build.yml

deploy:
	ansible-playbook -i ansible/inventory/hosts.yml ansible/playbooks/deploy.yml

all: build deploy 