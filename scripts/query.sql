-- main table
CREATE TABLE IF NOT EXISTS food_sup_data (
	id integer PRIMARY KEY,
	date text NOT NULL,
	production_order text NOT NULL,
	item text NOT NULL,
	production_line text NOT NULL,
	batch_number text NOT NULL,
	case_sn text NOT NULL,
	box_sn text NOT NULL
);

DROP TABLE food_sup_data;

SELECT * FROM food_sup_data WHERE production_order='ПР010011' AND batch_number='10122';