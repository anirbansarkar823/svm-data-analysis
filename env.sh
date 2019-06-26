SVM_DIR=~/Documents/svm
YML_DIR="$SVM_DIR/yaml"
YML_TMP="$YML_DIR/temp"
YML_ATR="$YML_DIR/attr_temp"
YML_WTV="$YML_DIR/weights_thresh_vals"
YML_ASS="$YML_DIR/assigned"
CSV_DIR="$SVM_DIR/csv"
CSV_OR="$CSV_DIR/original"
CSV_PR="$CSV_DIR/processed"
CSV_CLN="$CSV_DIR/cleaned"
CSV_SC="$CSV_DIR/score_sheets"

if [ ! -d "$YML_TMP" ];
then
	mkdir -p "$YML_TMP"
fi

if [ ! -d "$YML_ATR" ];
then
	mkdir -p "$YML_ATR"
fi

if [ ! -d "$YML_WTV" ];
then
	mkdir -p "$YML_WTV"
fi

if [ ! -d "$YML_ASS" ];
then
	mkdir -p "$YML_ASS"
fi

if [ ! -d "$CSV_OR" ];
then
	mkdir -p "$CSV_OR"
fi

if [ ! -d "$CSV_PR" ];
then
	mkdir -p "$CSV_PR"
fi

if [ ! -d "$CSV_CLN" ];
then
	mkdir -p "$CSV_CLN"
fi

if [ ! -d "$CSV_SC" ];
then
	mkdir -p "$CSV_SC"
fi

alias clean='python cleaning_pipeline.py'
alias gen_wtv='python gen_clean_final.py'
alias score='python scoring.py'

export SVM_DIR
export YML_TMP
export YML_ASS
export YML_DIR 
export YML_ATR
export YML_WTV
export CSV_DIR
export CSV_PR
export CSV_OR
export CSV_CLN
export CSV_SC
