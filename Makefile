

push: build
	docker push hub.sixtyfive.me/timeline_to_kml:latest

build:
	docker buildx build --platform linux/arm64,linux/amd64 -t hub.sixtyfive.me/timeline_to_kml .
