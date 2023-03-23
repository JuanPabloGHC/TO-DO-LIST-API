from flask import Flask, render_template, jsonify, abort, request

app = Flask(__name__)

uri = '/api/tasks'
persona = {'name': 'JP', 'matricula':'184429'}
#Lista para TO-DO LIST
tasks = [
    {
        'id': 1,
        'name': 'Cenar algo bien sabroso',
        'status': False
    },
    {
        'id': 2,
        'name': 'Limpiar la casa',
        'status': False
    },
]


@app.route("/")
def hello_world():
    return render_template('index.html', data=persona)

#API
@app.route(uri, methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route(uri + '/<int:id>', methods=['GET'])
def get_task(id):
    this_task = 0
    for task in tasks:
        if(task['id'] == id):
            this_task = task
    if this_task == 0:
        abort(404)
    return jsonify({'task': this_task})

@app.route(uri, methods=['POST'])
def create_task():
    #Se recibe un json?
    if request.json:
        if request.json['name'] != '':
            task = {
                'id': len(tasks) + 1,
                'name': request.json['name'],
                'status': False
            }
            tasks.append(task)

        return jsonify({'task': tasks}), 201
        # status: 200 -> OK, 201 -> ok de creación
    else:
        abort(404)

@app.route(uri + '/<int:id>', methods=['PUT'])
def update_task(id):
    #Se recibe un json?
    if request.json:
        #Buscar elemento con el id en la lista de tasks
        this_task = [task for task in tasks if task['id'] == id]
        #Si existe la tarea con el id
        if this_task:
            #Se recibe un name para actualizar
            if request.json.get('name'):
                this_task[0]['name'] = request.json['name']
            #Se recibe un status para actualizar
            if request.json.get('status') or not request.json.get('status'):
                this_task[0]['status'] = request.json['status']
        else:
            abort(404)        
    else:
        abort(404)
    
    return jsonify({'task': this_task[0]})

@app.route(uri + '/<int:id>', methods=['DELETE'])
def delete_task(id):
    #Buscar elemento con el id en la lista de tasks
    print(id)
    this_task = [task for task in tasks if task['id'] == id]
    print(this_task)
    if this_task:
        tasks.remove(this_task[0])
    else:
        abort(404)
    
    return jsonify({'tasks': tasks})


if __name__ == '__main__':
    app.run(debug=True)