

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('_user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    title_slug = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text)

    def __repr__(self):
        return f'<Post {self.title}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1
                self.title_slug = f'{self.title_slug}-{count}'

    def public_url(self):
        return url_for('show_post', slug=self.title_slug)

    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(title_slug=slug).first()

    @staticmethod
    def get_all():
        return Post.query.all()

class PostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=128)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Enviar')

@app.route("/admin/post/", methods=['GET', 'POST'], defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>/", methods=['GET', 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        post = Post(user_id=current_user.id, title=title, content=content)
        post.save()

        return redirect(url_for('index'))
    return render_template("admin/post_form.html", form=form)


@app.route("/p/<string:slug>/")
def show_post(slug):
    post = Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("post_view.html", post=post)

{% extends "base_template.html" %}

{% block title %}
    {% if form.title.data %}
        {{ form.title.data }}
    {% else %}
        Nueva entrada
    {% endif %}
{% endblock %}

{% block content %}
    <form action="" method="post" novalidate>
        {{ form.hidden_tag() }}
        <div>
            {{ form.title.label }}
            {{ form.title(size=128) }}<br>
            {% for error in form.title.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </div>
        <div>
            {{ form.content.label }}
            {{ form.content }}<br>
            {% for error in form.content.errors %}
            <span style="color: red;">{{ error }}</span>
            {% endfor %}
        </div>
        <div>
            {{ form.submit() }}
        </div>
    </form>
{% endblock %}
//el de arriba es el formulario
// ver post
{% extends "base_template.html" %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
    <h1>{{ post.title }}</h1>
    {{ post.content }}
{% endblock %}