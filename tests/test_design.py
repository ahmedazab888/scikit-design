from skdesign.design import block_design


def test_block_design():
    """ See http://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm """
    x_1 = [1, 2, 3, 4]
    x_2 = [1, 2, 3]
    design = [[1, 1],
              [1, 2],
              [1, 3],
              [2, 1],
              [2, 2],
              [2, 3],
              [3, 1],
              [3, 2],
              [3, 3],
              [4, 1],
              [4, 2],
              [4, 3]]

    res = block_design(x_1=x_1, x_2=x_2, randomize=False)
    assert res['names'] == ['x_1', 'x_2']
    assert res['names'] != ['x_2', 'x_1']
    assert res['design'] == design

    x_1 = [1, 2]
    x_2 = [1, 2, 3, 4]
    x_3 = [1, 2, 3]
    design = [[1, 1, 1],
              [1, 1, 2],
              [1, 1, 3],
              [1, 2, 1],
              [1, 2, 2],
              [1, 2, 3],
              [1, 3, 1],
              [1, 3, 2],
              [1, 3, 3],
              [1, 4, 1],
              [1, 4, 2],
              [1, 4, 3],
              [2, 1, 1],
              [2, 1, 2],
              [2, 1, 3],
              [2, 2, 1],
              [2, 2, 2],
              [2, 2, 3],
              [2, 3, 1],
              [2, 3, 2],
              [2, 3, 3],
              [2, 4, 1],
              [2, 4, 2],
              [2, 4, 3]]

    res = block_design(x_1=x_1, x_2=x_2, x_3=x_3, randomize=False)
    assert res['names'] == ['x_1', 'x_2', 'x_3']
    assert res['names'] != ['x_2', 'x_1', 'x_3']
    assert res['design'] == design
