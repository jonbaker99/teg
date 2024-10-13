from utils import get_ranked_teg_data, get_ranked_round_data, get_ranked_frontback_data,safe_ordinal
from utils import chosen_rd_context, chosen_teg_context

# ROUND CONTEXT

df = get_ranked_round_data()
max_teg_r = df.loc[df['TEGNum'].idxmax(), 'TEG']
max_rd_in_max_teg = df[df['TEG'] == max_teg]['Round'].max()

teg_r = max_teg_r
rd_r = max_rd_in_max_teg

print(chosen_rd_context(df,teg_r,rd_r,'Sc'))
print(chosen_rd_context(df,teg_r,rd_r,'GrossVP'))
print(chosen_rd_context(df,teg_r,rd_r,'NetVP'))
print(chosen_rd_context(df,teg_r,rd_r,'Stableford'))


# TEG CONTEXT

df = get_ranked_teg_data()
max_teg_t = df.loc[df['TEGNum'].idxmax(), 'TEG']
teg_t = max_teg_t

print(chosen_teg_context(df,teg_t,'Sc'))
print(chosen_teg_context(df,teg_t,'GrossVP'))
print(chosen_teg_context(df,teg_t,'NetVP'))
print(chosen_teg_context(df,teg_t,'Stableford'))
