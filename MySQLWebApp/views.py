from django.shortcuts import render
from .forms import DatabaseConnectionForm, SQLQueryForm
import MySQLdb as mysql

# Create your views here.

def database_connection(request):
    if request.method == 'POST':
        form = DatabaseConnectionForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            host = form.cleaned_data['host']
            port = form.cleaned_data['port']
            database_name = form.cleaned_data['database_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                # Establish a MySQL connection
                connection = mysql.connect(
                    host=host,
                    port=port,
                    database=database_name,
                    user=username,
                    passwd=password
                )

                request.session['db_connection_details'] = {
                    'host': host,
                    'port': port,
                    'database_name': database_name,
                    'username': username,
                    'password': password
                }

                # Get a cursor to execute queries
                cursor = connection.cursor()

                # Retrieve table names
                cursor.execute("SHOW TABLES")
                table_names = [row[0] for row in cursor.fetchall()]

                # Create a dictionary to store table data
                table_data = {}

                # Retrieve the first five rows of each table
                for table_name in table_names:
                    query = f"SELECT * FROM {table_name} LIMIT 5"
                    cursor.execute(query)
                    columns = [desc[0] for desc in cursor.description]  # Get column names
                    rows = cursor.fetchall()
                    table_data[table_name] = {'columns': columns, 'rows': [dict(zip(columns, row)) for row in rows]}
                print(table_data)

                # Close the cursor
                cursor.close()

                # Close the database connection
                connection.close()

                # Render a template to display the table names and their first five rows
                return render(request, 'data_display.html', {'table_names': table_names, 'table_data': table_data})


            except mysql.Error as err:
                # Handle connection errors
                error_message = f"Error: {err}"
                return render(request, 'error.html', {'error_message': error_message})

    else:
        form = DatabaseConnectionForm()
    return render(request, 'database_connection.html', {'form': form})


def execute_query(request):
    if request.method == 'POST':
        form = SQLQueryForm(request.POST)

        if form.is_valid():
            sql_query = form.cleaned_data['sql_query']

        # Retrieve connection details from the session
        connection_details = request.session.get('db_connection_details')

        if connection_details:
            host = connection_details['host']
            port = connection_details['port']
            database_name = connection_details['database_name']
            username = connection_details['username']
            password = connection_details['password']

            try:
                # Establish a MySQL connection using the retrieved details
                connection = mysql.connect(
                    host=host,
                    port=port,
                    database=database_name,
                    user=username,
                    passwd=password
                    )
                # Get a cursor to execute queries
                cursor = connection.cursor()

                # Execute the SQL query
                cursor.execute(sql_query)

                # Fetch the results
                query_result = cursor.fetchall()
                # Get column names
                columns = [desc[0] for desc in cursor.description]

                # Close the cursor and database connection
                cursor.close()
                connection.close()

                # Format the query result
                formatted_query_result = {
                    'columns': columns,
                    'rows': [dict(zip(columns, row)) for row in query_result]
                }

                return render(request, 'query_result.html', {'formatted_query_result': formatted_query_result})


            except mysql.Error as err:
                error_message = f"Error: {err}"
                return render(request, 'error.html', {'error_message': error_message})
    else:
        form = SQLQueryForm()

    return render(request, 'query_execution.html', {'form': form})
