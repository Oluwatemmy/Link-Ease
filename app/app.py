from link_ease import create_app
from app.link_ease.settings import config_dict

app = create_app(config=config_dict['prod'])

if __name__ == "__main__":
    app.run(debug=True)