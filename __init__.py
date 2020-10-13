import statistics

def calc_conditional_avg(**data):
    entity_id = data.get('entity_id', None)
    if entity_id is None:
        log.error('entity_id is required')
        return
    friendly_name = data.get('friendly_name', '')
    unit_of_measurement = data.get('unit_of_measurement', '')

    conditions = list(data['conditions'])
    precision = data.get('precision',0)

    # wait for any other updates to come in
    task.unique('calc_conditional_avg_{}'.format(entity_id))
    task.sleep(3)

    all_values = []
    values = []
    included = []
    all_included = []
    for condition_row in conditions:
        try:
            row_value = float(state.get(condition_row['entity']))
            condition_value = state.get(condition_row['condition']) == 'on'
        except Exception as e:
            log.error('Invalid Condition Row')
            log.error(f'Exception: {e}')
            log.error(f'Row: {condition_row}')
            continue
        all_values.append(row_value)
        all_included.append(condition_row['entity'])
        if condition_value:
            values.append(row_value)
            included.append(condition_row['entity'])
    
    if len(values) > 0:
        values_actual = values
        included_actual = included
    else:
        values_actual = all_values
        included_actual = all_included

    result = round(statistics.mean(values_actual),precision)

    log.debug('avg: {}'.format(result))

    state.set(entity_id, result, new_attributes={
        'unit_of_measurement': unit_of_measurement,
        'friendly_name': friendly_name,
        'sensors': included_actual,
        'values': values_actual,
    })


registered_triggers = []

def register_calc_conditional_avg(data):
    log.error(f'loading calc_conditional_avg for {data["entity_id"]}')
    conditions = list(data['conditions'])

    watch_entities = []
    for condition in conditions:
        watch_entities.append(condition['condition'])
        watch_entities.append(condition['entity'])
    
    @time_trigger("startup")
    @state_trigger('True or {}'.format(" or ".join(watch_entities)))
    def inner_function():
        nonlocal data
        calc_conditional_avg(**data)

    registered_triggers.append(inner_function)

##########
# Helpers
##########
def load_app(app_name, factory):
    if "apps" not in pyscript.config:
        return
    
    if app_name not in pyscript.config['apps']:
        return

    for app in pyscript.config['apps'][app_name]:
        log.info(f'loading {app_name} app with config {app}')
        factory(app)

def load_app_list(app_name, factory):
    if "apps_list" not in pyscript.config:
        return

    for app in pyscript.config['apps_list']:
        if 'app' not in app:
            continue
    
        if app['app'] == app_name:
            factory(app)

##########
# Startup
##########
@time_trigger('startup')
def load():
    load_app('calc_conditional_avg', register_calc_conditional_avg)
    load_app_list('calc_conditional_avg', register_calc_conditional_avg)