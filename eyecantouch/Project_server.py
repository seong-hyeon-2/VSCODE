from flask import Flask, request, redirect
import random


app = Flask(__name__)


nextId = 4
# 원래는 데이터베이스에 저장됨. 왜냐하면 데이터 양이 엄청 많기 때문
topics = [
  {'id' : 1, 'title' : 'html', 'body' : 'html is ...'},
  {'id' : 2, 'title' : 'css', 'body' : 'css is ...'},
  {'id' : 3, 'title' : 'javascript', 'body' : 'javascript is ...'}
]


def template(contents, content, id=None):
  contextUI = ''
  if id != None:
      contextUI = f'''
        <li><a href="/update/{id}/">update</a></li>
        <li><form action="/delete/{id}" method="POST"><input type="submit" value="delete"></form></li>
      '''
  # return 값은 문자열이어야함
  # ''' -> 여러 줄을 쓰기 위해서
  return f'''<!doctype html>
  <html>
    <body>
      <h1><a href="/">WEB</a><h1>
      <ol>
        {contents}
      </ol>
      {content}
      <ul>
        <li><a href="/create/">create</a></li>
        {contextUI}
      </ul>  
    </body>
  </html>
  '''

def getContents():
  liTags = ''
  for topic in topics:
    # a태그 -> 링크 걸어주는 것(내용도 포함)
    liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
  return liTags

# routing
@app.route('/')
def index():
  return template(getContents(), '<h2>Welcome</h2>Hello, Web')


# routing
@app.route('/read/<int:id>/')
def read(id):
  title = ''
  body = ''
  for topic in topics:
    if id == topic['id']:
      title = topic['title']
      body = topic['body']
      break
      newTopic = {'title': title, 'body': body}
  return template(getContents(), f'<h2>{title}</h2>{body}', id)



@app.route('/create/', methods=['GET', 'POST'])
def create():
  if request.method == 'GET':
    # input = text 정보를 서버로 전송할 때 사용자에게 입력받는 함수
    # form 태그는 사용자가 입력한 정보를 서버로 전송하는 역할
    # action : 서버에 어떤 경로로 전송할 것인가
    # name : 각각의 값을 어떤 이름으로 전송할 것인지
    # get방식 : URL을 통해서 데이터를 전송하는 방식 - 아래와 같은 방식
    # 동적으로 동작하는 웹서비스에서 특정한 페이지를 식별하는 고유한 주소로써 사용되는 방식
    
    # method의 기본은 GET, 데이터를 수정할 때 사용하고 싶으면 -> POST
    # POST를 이용하면 데이터가 URL을 통해서 전송되지 않음 -> URL에 서버로 전송한 데이터가 포함되어있지 않음
    # 웹브라우저가 서버한테 전송한 데이터는 보이지 않고 은밀하게 감춰진 상태로 보내져 URL에 보이지 않음
    # 훨씬 더 큰 데이터를 안전하게 전송할 수 있음
    content = '''
    <form action="/create/" method="POST">
      <p><input type="text" name='title' placeholder="title"></p>
      <p><textarea name='body' placeholder='body'></textarea></p>
      <p><input type="submit" value="create"></p>
    </form>
    '''
    return template(getContents(), content)
  elif request.method == 'POST':
    global nextId
    title = request.form['title']
    body = request.form['body']
    newTopic = {'id': nextId, 'title': title, 'body':body}
    topics.append(newTopic)
    url = '/read/'+ str(nextId) + '/'
    nextId = nextId + 1
    # redirect를 쓰면 사용자의 웹브라우저한테 어디로 이동하라고 명령을 내릴 수 있음
    return redirect(url)
 


# update는 id값을 파라미터로 받아야하기 때문에, int해줘야함
# update는 create와 비숫한데 read 부분도 필요함
@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
  if request.method == 'GET':
    title = ''
    body = ''
    for topic in topics:
      if id == topic['id']:
        title = topic['title']
        body = topic['body']
        break
    content = f'''
    <form action="/update/{id}/" method="POST">
      <p><input type="text" name='title' placeholder="title" value="{title}"></p>
      <p><textarea name='body' placeholder='body'>{body}</textarea></p>
      <p><input type="submit" value="update"></p>
    </form>
    '''
    return template(getContents(), content)
  elif request.method == 'POST':
    global nextId
    title = request.form['title']
    body = request.form['body']
    for topic in topics:
      if id == topic['id']:
        topic['title'] = title
        topic['body'] = body
        break
    url = '/read/'+ str(nextId) + '/'
    # redirect를 쓰면 사용자의 웹브라우저한테 어디로 이동하라고 명령을 내릴 수 있음
    return redirect(url)


# delete
@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
  for topic in topics:
    if id == topic['id']:
      topics.remove(topic)
      break
  return redirect('/')



# port : 5001, debug : 자동으로 갱신 
app.run(port=5001, debug=True)



