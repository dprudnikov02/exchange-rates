insert into exchange_rates (base, target, ts, rate)
values ({{'\'' + ti.xcom_pull(task_ids='transform', key='latest_rate')|join('\', \'') + '\''}})