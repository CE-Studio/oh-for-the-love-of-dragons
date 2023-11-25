extends GraphEdit


var _errorico = {
    "ok": preload("res://compiler/ok.png"),
    "warning": preload("res://compiler/warning.png"),
    "error": preload("res://compiler/stop.png")
}


# Called when the node enters the scene tree for the first time.
func _ready():
    pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
    pass


func _on_popup_request(position):
    $"../../../NodeList".position = position
    $"../../../NodeList".visible = true
    verify()
    
    
func reposition(i:GraphNode):
    i.position_offset = (get_viewport().get_mouse_position() + scroll_offset - position) / zoom
    verify()


func verify():
    var stat := ["ok", "No errors"]
    for i in get_children():
        var j = i.verify()
        if j[0] != "ok":
            stat = j
            break
    $"../Button".text = stat[1]
    $"../Button".icon = _errorico[stat[0]]


func _on_connection_request(from_node:StringName, from_port:int, to_node:StringName, to_port:int):
    for i in get_connection_list():
        if (i.from_node == from_node) and (from_port == i.from_port):
            return
    connect_node(from_node, from_port, to_node, to_port)
    verify()


func _on_disconnection_request(from_node, from_port, to_node, to_port):
    disconnect_node(from_node, from_port, to_node, to_port)
    verify()
