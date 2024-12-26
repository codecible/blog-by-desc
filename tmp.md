 curl -X POST \
  http://127.0.0.1:3001/blog/generate \
  -H "Content-Type: application/json" \
  -d '{"description":"1234132412341234","core_idea":"2341234"}'


在 Vite 的生产环境（vite preview）中，环境变量需要在构建时（build time）就被注入，而不是在运行时（runtime）加载。我们现在的配置有两个问题：
.env.production 文件是在运行时通过 docker-compose 加载的，这对已经构建好的前端代码来说太晚了
docker-compose.yml 中的环境变量也是在运行时加载的，同样太晚了


docker-compose build frontend --no-cache
docker-compose up -d frontend