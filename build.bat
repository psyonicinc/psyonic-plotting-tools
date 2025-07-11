docker build -t psyonic-plotting-tools .
docker run --rm -v %cd%:/host psyonic-plotting-tools /bin/bash -c "cp /app/dist/plot-lines /host/dist/"