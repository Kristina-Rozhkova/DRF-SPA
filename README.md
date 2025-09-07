# Backend для сайта онлайн-школы

**Контекст:**
В мире развивается тренд на онлайн-обучение. Но для веб-разработчика важно не только обучиться, но и знать, как
реализовать платформу для онлайн-обучения. Поэтому новая задача касается разработки LMS-системы, в которой каждый
желающий может размещать свои полезные материалы или курсы.
Ранее в проектах мы могли сразу видеть визуальное отображение результата разработки, теперь работа будет над SPA
веб-приложением и результатом создания проекта будет бэкенд-сервер, который возвращает клиенту JSON-структуры.

# Инструкция по настройке удаленного сервера и деплою проекта.

1. Подготовка сервера

    Требования:
    - Сервер с ОС Ubuntu 22.04 LTS (или аналогичной)
    - Установленные инструменты: Docker, Docker Compose, Git

2. Настройка сервера

   - Подключение к серверу
        ```bash
        ssh study-pltform 89.169.182.8
        ```
    - Установка Docker и Docker Compose
        ```bash
        sudo apt update
        sudo apt install -y docker.io docker-compose
        sudo systemctl enable docker
        sudo usermod -aG docker $USER  # Добавляем текущего пользователя в группу docker
        newgrp docker  # Применяем изменения
        ```
    - Установка Git
        ```bash
        sudo apt install -y git
        ```

3. Деплой проекта
    - Клонирование репозитория
       ```bash
       git clone https://github.com/ваш-username/DRF-SPA.git
       cd DRF-SPA
       ```
    - Настройка переменных окружения
    
       Скопируйте .env.sample в .env и заполните значения:
       ```bash
       cp .env.sample .env
       nano .env  # Редактируем файл
       ```
    - Запуск проекта
       ```bash
       docker-compose up -d --build
       ```
    - Workflow (CI/CD)
       - Настройка GitHub Actions

         Создайте файл .github/workflows/deploy.yml:
         ```yaml
         name: Deploy DRF-SPA

         on:
          push:
            branches: [ main ]
        
         jobs:
          deploy:
            runs-on: ubuntu-latest
            steps:
              - name: Checkout code
                uses: actions/checkout@v2
        
              - name: Install SSH key
                uses: shimataro/ssh-key-action@v2
                with:
                  key: ${{ secrets.SSH_PRIVATE_KEY }}
                  known_hosts: ${{ secrets.KNOWN_HOSTS }}
        
              - name: Deploy via SSH
                run: |
                  ssh ваш_пользователь@IP_сервера "cd DRF-SPA && git pull && docker-compose up -d --build"
          ```
       - Добавление Secrets в GitHub

       - `DEPLOY_DIR`               Путь к директории проекта на сервере (например, `/home/user/DRF-SPA`).  | 
       - `DOCKER_HUB_ACCESS_TOKEN`  Токен доступа к Docker Hub (для push/pull образов).                     |
       - `DOCKER_HUB_USERNAME`      Логин в Docker Hub.                                                    | 
       - `SERVER_ID`                IP-адрес или домен сервера для деплоя.                                 |
       - `SSH_KEY`                  Приватный SSH-ключ для доступа к серверу.                              |
       - `SSH_USER`                 Имя пользователя на сервере (например, `root` или `deploy`).
    
   - Команды для управления

       - Перезапуск контейнеров - docker-compose restart
       - Просмотр логов - docker-compose logs -f
       - Остановка проекта - docker-compose down
       - Обновление кода - git pull && docker-compose up -d --build

   - Тестирование

        Откройте в браузере:
        
        http://89.169.182.8 — главная страница.
        
        http://89.169.182.8/admin — админка Django.