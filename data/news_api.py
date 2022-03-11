import json

import flask
from flask import jsonify, request

from . import db_session
from .news import News

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='../templates'
)


@blueprint.route('/api/news')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('title', 'content', 'user.name')) for item in news]
        }
    )

@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == news_id).first()
    if not news:
        return jsonify({'error':'Not found!'})
    return jsonify(
        {
            'news':
                news.to_dict(only=('title', 'content', 'user.name'))
        }
    )

@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    x = json.loads(request.json)
    news = News(
        title=x['title'],
        content=x['content'],
        user_id=x['user_id'],
        is_private=x['is_private']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


