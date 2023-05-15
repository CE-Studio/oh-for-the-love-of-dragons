extends GraphEdit


# Called when the node enters the scene tree for the first time.
func _ready():
    pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
    pass


func _on_popup_request(position):
    $"../../NodeList".position = position
    $"../../NodeList".visible = true
    
    
func reposition(i:GraphNode):
    i.position_offset = (get_viewport().get_mouse_position() + scroll_offset - position) / zoom


func _on_connection_request(from_node:StringName, from_port:int, to_node:StringName, to_port:int):
    for i in get_connection_list():
        if (i.from == from_node) and (from_port == i.from_port):
            return
    connect_node(from_node, from_port, to_node, to_port)


func _on_disconnection_request(from_node, from_port, to_node, to_port):
    disconnect_node(from_node, from_port, to_node, to_port)
