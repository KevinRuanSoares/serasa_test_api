debug:
	docker-compose -f docker-compose.yml -f docker-compose-debug.yml up --build

local:
	docker-compose -f docker-compose.yml up --build

run-server:
	docker-compose -f docker-compose-deploy.yml up -d

stop-server:
	docker-compose -f docker-compose-deploy.yml down

update-app:
	git pull origin
	docker-compose -f docker-compose-deploy.yml build app
	docker-compose -f docker-compose-deploy.yml up --no-deps -d app

update-server:
	git pull origin
	docker-compose -f docker-compose-deploy.yml build proxy
	docker-compose -f docker-compose-deploy.yml up --no-deps -d proxy

logs:
	docker-compose -f docker-compose-deploy.yml logs
	
style:
	docker-compose run --rm app sh -c "black --line-length 120 app/"
	docker-compose run --rm app sh -c "flake8 --max-line-length=120"

test:
	docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py test"

remove-continers:
	docker stop $(docker ps -aq) && docker rm $(docker ps -aq) && docker volume rm $(docker volume ls -q) && docker system prune -a

proxy-terminal:
	docker exec -ti django_api_model_proxy_1 sh

app-terminal:
	docker exec -ti django_api_model-app-1 sh

makemessages:
	docker-compose run --rm app sh -c "django-admin makemessages -l pt_BR"

compilemessages:
	docker-compose run --rm app sh -c "django-admin compilemessages"

makemigrations:
	docker-compose run --rm app sh -c "python manage.py makemigrations"

migrate:
	docker-compose run --rm app sh -c "python manage.py migrate"

createsuperuser:
	docker-compose run --rm app sh -c "python manage.py createsuperuser"