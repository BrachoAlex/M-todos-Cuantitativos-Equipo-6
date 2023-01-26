import random
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from tabulate import tabulate

# openpyxl also required; XLSX export
# PANDAS PRINT FIX
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)


def cashier_simulator(number_of_clients, maximum_time_client, maximum_time_operation):
    # Init starting times
    client_arrival_time = datetime(2023, 1, 24, 9, 00)
    services_start = datetime(2023, 1, 24, 9, 00)
    original_services_start = datetime(2023, 1, 24, 9, 00)
    # Init variables
    client_number = 1
    time_between_arrivals = 0
    waiting_time = 0
    cashier_inactivity = 0
    operations_time_total = 0
    wait_client_total = 0
    inactivity_cashier_total = 0
    total_clients_waited = 0
    index = 1
    # Data frame creation
    df = pd.DataFrame(columns=["Cliente", "Tiempo entre llegadas", "Hora de llegada", "Tiempo del trámite",
                               "Inicia servicio", "Termina Servicio", "Tiempo de espera de cliente",
                               "Tiempo de inactividad del ATM"])

    # Base Case
    time_operation = random.randint(1, maximum_time_operation)
    operations_time_total += time_operation
    services_end = services_start + timedelta(minutes=time_operation)
    df.loc[index] = [client_number, time_between_arrivals, datetime.strftime(client_arrival_time, "%H:%M %p"),
                     time_operation, datetime.strftime(services_start, "%H:%M %p"),
                     datetime.strftime(services_end, "%H:%M %p"), waiting_time, cashier_inactivity]
    index += 1

    while number_of_clients != 1:
        time_operation = random.randint(1, maximum_time_operation)
        operations_time_total += time_operation
        time_between_arrivals = random.randint(1, maximum_time_client)
        client_arrival_time = client_arrival_time + timedelta(minutes=time_between_arrivals)
        client_number += 1
        if services_end > client_arrival_time:
            cashier_inactivity = 0
            services_start = services_end
        else:
            services_start = client_arrival_time
            cashier_inactivity = client_arrival_time.minute - services_end.minute
            if cashier_inactivity < 0:
                cashier_inactivity = 60 - abs(cashier_inactivity)
            inactivity_cashier_total += cashier_inactivity
        waiting_time = services_start.minute - client_arrival_time.minute
        if waiting_time < 0:
            waiting_time = 60 - abs(waiting_time)
        wait_client_total += waiting_time
        if waiting_time > 0:
            total_clients_waited += 1
        services_end = services_start + timedelta(minutes=time_operation)
        df.loc[index] = [client_number, time_between_arrivals, datetime.strftime(client_arrival_time, "%H:%M %p"),
                         time_operation, datetime.strftime(services_start, "%H:%M %p"),
                         datetime.strftime(services_end, "%H:%M %p"), waiting_time, cashier_inactivity]
        index += 1
        number_of_clients -= 1

    average_wait = wait_client_total / client_number
    wait_probability = (total_clients_waited / client_number) * 100
    total_simulation_time = (client_arrival_time - original_services_start).total_seconds() / 60
    inactive_percentage = (inactivity_cashier_total / total_simulation_time) * 100
    average_wait_for_service = operations_time_total / client_number
    # ANNEXING TOTALS
    df.loc[index] = ["TOTAL:", "", str(total_simulation_time) + " min", operations_time_total, "", "",
                     wait_client_total, inactivity_cashier_total]
    # DATAFRAME FORMAT
    pdtabulate = lambda df: tabulate(df, headers='keys', tablefmt='psql', showindex=False)
    print(pdtabulate(df))
    # Write to CSV/XLSX; XLSX looks better
    writer = pd.ExcelWriter('myDataFrame.xlsx')
    df.to_excel(writer, 'DataFrame')
    writer.save()
    # NOTE: IGNORE SAVE ERROR

    print("Tiempo de espera promedio por cliente: " + str(
        round(average_wait, 2)) + " minutos de espera para ser atendidos")
    print("Probabilidad de que un cliente espere en la fila: " + str(round(wait_probability, 2)) + "%")
    print("Porcentaje de tiempo en que el ATM estuvo inactivo: " + str(round(inactive_percentage, 2)) + "%")
    print("Tiempo promedio de servicio: " + str(round(average_wait_for_service, 2)) + " minutos de realizar el trámite")


cashier_simulator(20, 35, 35)
