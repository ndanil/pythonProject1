from flask import jsonify
from flask_restful import abort, Resource, reqparse

from data import db_session
from data.news import News


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return jsonify({'news': news.to_dict(
            only=('title', 'content', 'user_id', 'is_private'))})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True)
    parser.add_argument('content')
    parser.add_argument('is_private')
    parser.add_argument('user_id')
    def get(self):
        session = db_session.create_session()
        news = session.query(News).all()
        return jsonify({'news': [d.to_dict(
            only=('title', 'content', 'user_id', 'is_private')) for d in news]})
    def post(self):
        args = self.parser.parse_args()
        sess = db_session.create_session()
        news = News(
            title=args['title'],
            content=args['content']

        )
        sess.add(news)
        sess.commit()
        return jsonify({'success': 'OK'})
