
if __name__ == '__main__':
    import argparse
    import pandas as pd

    from svm_data_clean import clean_dframe, generate_doc

    parser = argparse.ArgumentParser(description='Generate LaTeX document from SVM data.')
    parser.add_argument('-i', help='path of input csv file containing svm data.')
    parser.add_argument('-a', help='Asset name.')
    parser.add_argument('-v', help='Vertical name.')
    args = parser.parse_args()
    csv_input = args.i
    vert = args.v
    asset = args.a
    df = pd.read_csv(csv_input)
    df = clean_dframe(df, {'vertical':vert, 'asset_name':asset})
    generate_doc(df)
