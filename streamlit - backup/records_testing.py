import pandas as pd
from utils import aggregate_data, format_vs_par

# Load the data from the Parquet file & exclude teg 2 and 50
all_data = pd.read_parquet('../data/all-data.parquet')
all_data = all_data[~all_data['TEG'].isin(['TEG 2', 'TEG 50'])]



def find_best_rows(data, level_of_aggregation, fields_to_keep, field='GrossVP', top_n=10):
    # Aggregate the data based on the provided level of aggregation
    aggregated_data = aggregate_data(data, level_of_aggregation)
    
    # Define properties for each field
    field_properties = {
        'GrossVP': {'new_name': 'Gross', 'ascending': True, 'formatter': format_vs_par, 'additional_field': 'Sc'},
        'NetVP': {'new_name': 'Net', 'ascending': True, 'formatter': format_vs_par, 'additional_field': None},
        'Sc': {'new_name': 'Gross Score', 'ascending': True, 'formatter': lambda x: int(x), 'additional_field': 'GrossVP'},
        'Stableford': {'new_name': 'Stableford', 'ascending': False, 'formatter': lambda x: int(x), 'additional_field': None},
    }
    
    fields_to_keep = fields_to_keep.copy()


    # Get the properties for the selected field
    properties = field_properties.get(field)
    if not properties:
        raise ValueError(f"Invalid field: {field}")
    
    # Append additional_field to fields_to_keep if it's not None
    additional_field = properties['additional_field']
    #print(f"\nField is: {field};\n additional_field is: {additional_field}\nfields to keep: {fields_to_keep}")

    fields_to_keep += [additional_field] if additional_field else []

    #print(f"\nfields to keep: {fields_to_keep}\n")
    #print(f"All fields pre update: {all_fields if 'all_fields' in locals() else 'all_fields does not exist'}")

    all_fields = fields_to_keep + [field]

    #print(f"\nall_fields: {all_fields}")


    # Sort the data based on the 'ascending' property
    sorted_data = (aggregated_data[all_fields]
                   .sort_values(by=field, ascending=properties['ascending'])
                   .head(top_n))

    # Add ranking column (ranking order follows the 'ascending' property)
    sorted_data['Rank'] = sorted_data[field].rank(ascending=properties['ascending'], method='min').astype(int).astype(str)
    sorted_data.loc[sorted_data.duplicated('Rank', keep=False), 'Rank'] += '='
    
    # Reorder and rename columns
    sorted_data = sorted_data[['Rank'] + all_fields]
    sorted_data.rename(columns={field: properties['new_name']}, inplace=True)
    
    # Apply formatting to the chosen field
    sorted_data[properties['new_name']] = sorted_data[properties['new_name']].apply(properties['formatter'])
    
    # Apply formatting to all numeric columns
    sorted_data = sorted_data.applymap(lambda x: int(x) if isinstance(x, (int, float)) else x)

    return sorted_data

n_keep = 10
rd_fields = ['Player', 'TEG', 'Round']

lowest_rounds_gross = find_best_rows(all_data,'Round',rd_fields,'GrossVP' ,n_keep)
print('\nBest Gross')
print(lowest_rounds_gross)

lowest_rounds_sc = find_best_rows(all_data,'Round',rd_fields,'Sc' ,n_keep)
print('\nBest Score')
print(lowest_rounds_sc)

lowest_rounds_net = find_best_rows(all_data,'Round',rd_fields,'NetVP' ,n_keep)
print('\nBest Net')
print(lowest_rounds_net)

best_rounds_stableford = find_best_rows(all_data,'Round',rd_fields,'Stableford' ,n_keep)
print('\n=======\nBest Stableford\n========')
print(best_rounds_stableford)