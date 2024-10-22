from sqlalchemy import MetaData, Table, Column, Integer, String, LargeBinary

metadata=MetaData()

user=Table(
    'user',
    metadata,
    Column('id',Integer,primary_key=True),
    Column('email',String,nullable=False,unique=True),
    Column('username',String,nullable=False),
    Column('hashed_password',String,nullable=False)
)

pictur=Table( 
    'picture',
    metadata,
    Column('id',Integer,primary_key=True),
    Column('binary_picture',LargeBinary,nullable=False)
)