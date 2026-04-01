demo_data:
	python src/demo_setup.py

data_prep:
	python src/data_prep.py

model_lreg:
	python src/logistic_regression.py

model_rf:
	python src/random_forest.py

rpt_data:
	python reporting/rpt_data_setup.py

run_dev: 
	cd reporting/client; npm run dev

eda:
	python src/eda.py

dim_reduct:
	python src/dimensionality_reduction.py

