FROM nginx:stable-alpine

# Simple Dockerfile for reverse proxy. In production, add ModSecurity + OWASP CRS.
COPY conf /etc/nginx/conf.d
RUN mkdir -p /var/log/nginx

EXPOSE 80 443
