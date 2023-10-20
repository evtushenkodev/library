FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf
COPY library.nginx.conf /etc/nginx/sites-available/library.nginx.conf
RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/library.nginx.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]
