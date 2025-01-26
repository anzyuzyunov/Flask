import flask
from flask import jsonify, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from models import Ann, Session


app = flask.Flask('app')




class HttpError(Exception):

    def __init__(self, status_code: int , message: str | dict| list):
        self.status_code = status_code
        self.message = message



@app.errorhandler(HttpError)
def eror_handler(err: HttpError):
    response = jsonify({"erorr": err.message})
    response.status_code = err.status_code
    return response



def get_ann(session: Session, ann_id: int):
    ann = session.get(Ann, ann_id)
    if ann is None:
        raise HttpError(404,{"erorr": "announcement not found"})

    return ann

def post_ann(session: Session, ann: Ann):
    try:
        session.add(ann)
        session.commit()
    except IntegrityError:
        raise HttpError(409,message={"erorr": "need a unique description "})




class Announcement(MethodView):

    def post(self):
        ann_json = request.json
        with Session() as session:
            ann = Ann(title=ann_json['title'],description=ann_json['description'],owner=ann_json['owner'])
            post_ann(session, ann)
            return jsonify(ann.id_dict)


    def get(self, ann_id: int):
        with Session() as session:
            ann = get_ann(session, ann_id)
            return jsonify(ann.dict)


    def patch(self, ann_id: int):

        with Session() as session:
            ann_json = request.json
            ann = get_ann(session, ann_id)
            for title, description in ann_json.items():
                setattr(ann, title, description)
            post_ann(session, ann)
            return jsonify({"status": "Changes applied"})






    def delete(self,ann_id: int):
        with Session() as session:
            ann = get_ann(session, ann_id)
            session.delete(ann)
            session.commit()
            return jsonify({"status": "entry deleted"})



announcement_view = Announcement.as_view('ann')


app.add_url_rule(
    '/api/v1/ann', view_func= announcement_view, methods=['POST']
)

app.add_url_rule(
    '/api/v1/ann/<int:ann_id>', view_func= announcement_view, methods=['GET','DELETE', 'PATCH']
)


app.run()