from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tesla.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_mark = db.Column(db.String(3))
    username = db.Column(db.String(30))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Review %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/biography')
def bio():
    return render_template('biography.html')


@app.route('/about-me')
def feedback():
    return render_template('about-me.html')


@app.route('/inventions')
def inv():
    return render_template('inventions.html')


@app.route('/legacy')
def leg():
    return render_template('legacy.html')


@app.route('/reviews/<int:id>/')
def full_review(id):
    review = Review.query.get(id)
    return render_template('review_detail.html', review=review)


@app.route('/reviews/delete/<int:id>')
def delete(id):
    review_to_delete = Review.query.get_or_404(id)
    try:
        db.session.delete(review_to_delete)
        db.session.commit()
        return redirect('/reviews')
    except:
        return 'An error accured deleting the review'


@app.route('/reviews/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    review = Review.query.get_or_404(id)
    if request.method == 'POST':
        review.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/reviews')
        except:
            return 'An error occured updating the review.'
    else:
        return render_template('update.html', review=review)

@app.route('/reviews')
def reviews():
    reviews = Review.query.order_by(Review.date.desc()).all()
    return render_template('reviews.html', reviews=reviews) 


@app.route('/writing-a-review', methods=['POST', 'GET'])
def writing_a_review():
    if request.method == 'POST':
        username = request.form.get('username')
        content = request.form.get('content')
        module_mark = request.form.get('module_mark')
        user_review = Review(username=username, content=content, module_mark=module_mark)
        try:
            db.session.add(user_review)
            db.session.commit()
            return redirect('/')
        except:
            return 'An error occurred adding the review'
    else:
        return render_template('making-review.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
