extends OptionButton


func _on_item_selected(index):
    $"../Label2".text = ["to", "by"][index]
