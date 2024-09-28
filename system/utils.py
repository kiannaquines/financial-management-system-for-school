def oneshot_view_function(model, header_title, title, add_button_name, path, header_list, field_list):
    context = {}
    view_data = model.objects.values(*field_list)
    context['view_data'] = view_data
    context['header_title'] = header_title
    context['title'] = title
    context['add_button_name'] = add_button_name
    context['path'] = path
    context['header_list'] = header_list
    return context

def oneshot_add_function(form, header_title, title, add_button_name):
    context = {}
    context['form'] = form
    context['header_title'] = header_title
    context['title'] = title
    context['add_button_name'] = add_button_name
    return context