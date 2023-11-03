programa := tp
template := template-tp.tex
config   := config.yaml

all:
	pandoc \
		$(programa).md \
		-o $(programa).pdf \
		--metadata-file=$(config) \
		--template $(template)
