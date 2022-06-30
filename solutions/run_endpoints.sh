docker build -t music_style_image .
docker run --env-file=.env -i -t -p 8080:8080 --name music_style -v "/${PWD}"/src:/code/src music_style_image bash -c "python src/spotify.py"

# docker build -t music_style_image .
# docker run --env-file=.env -i -t -p 8080:8080 --name music_style -v "/${PWD}"/src:/code/src music_style_image bash -c "uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload"
# docker tag music_style_image:latest karlijnschipper/pyladies_fastapi:latest
# docker push karlijnschipper/pyladies_fastapi:latest
