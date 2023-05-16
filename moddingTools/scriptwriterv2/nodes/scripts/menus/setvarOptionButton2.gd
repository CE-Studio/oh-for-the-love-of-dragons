extends OptionButton


func _on_item_selected(index):
    $"../LineEdit2".placeholder_text = ["Value", "Name"][index]
