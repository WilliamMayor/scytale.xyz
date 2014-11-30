from scytale import create_app

config = {}
if __name__ == '__main__':
    with open('.env', 'rb') as fd:
        config.update(dict([l.split('=', 1) for l in fd.readlines()]))

app = create_app(config)

if __name__ == '__main__':
    app.run(debug=True)
