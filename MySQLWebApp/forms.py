from django import forms

class DatabaseConnectionForm(forms.Form):
    host = forms.CharField(label='Database Host', max_length=100)
    port = forms.IntegerField(label='Port', initial=3306)
    database_name = forms.CharField(label='Database Name', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class SQLQueryForm(forms.Form):
    sql_query = forms.CharField(label='Enter SQL Query', widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
