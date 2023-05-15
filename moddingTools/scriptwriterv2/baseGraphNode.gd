extends GraphNode
class_name BaseGraphNode


# Called when the node enters the scene tree for the first time.
func _ready():
    connect("close_request", _close)


func _close():
    var h:GraphEdit = get_parent()
    for i in h.get_connection_list():
        if (i["to"] == name) or (i["from"] == name):
            h.disconnect_node(i["from"], i["from_port"], i["to"], i["to_port"])
    queue_free()
