class ChoiceList extends React.Component {
    state = {
        listItems: new Array(this.props.initialListItems).fill(0)
    }

    oneChangeHandler = (e) => {
        let listItems = this.state.listItems
        for (let i = 0; i < listItems.length; i++) {
            if (i < e.target.value) {
                listItems[i] = 1
            } else {
                listItems[i] = 0
            }
        }
        for (let i = 0; i < listItems.length; i++) {
            if (listItems[i] === 0) {
                document.getElementById("group_" + (i).toString() + "1").checked = true
                document.getElementById("group_" + (i).toString() + "0").checked = false
            } else {
                document.getElementById("group_" + (i).toString() + "1").checked = false
                document.getElementById("group_" + (i).toString() + "0").checked = true

            }

        }
        document.getElementById("binary_choice_list_choose_risky").value = e.target.value
        if (e.target.value < listItems.length) {
            document.getElementById("feedback").innerHTML = `
            You indicate that you prefer any certain amount (Option B) that is bigger than or equal to $${e.target.value} over the lottery (Option A).
            `
        } else {
            document.getElementById("feedback").innerHTML = `
            You indicate that you prefer none of the offered certain amounts (Option B) over the lottery (Option A).
            `
        }
    }

    render() {
        let rows = []
        let prob_down = 100 - this.props.prob_up
        for (let i = 0; i < this.state.listItems.length; i++) {
            rows.push(
                <tr>
                    <td className="text-center align-middle">
                        <input type="radio" onClick={this.oneChangeHandler} id={"group_" + i + "0"} value={i + 1} name={"group_" + i} /> &emsp;
                        <input type="radio" onClick={this.oneChangeHandler} id={"group_" + i + "1"} value={i} name={"group_" + i} />
                    </td>
                    <td className="text-center align-middle">With certainty: <strong>Get ${this.props.listLabels[i]}</strong></td>
                </tr>
            )
        }
        return (
            <div id="decision_table">
                <table className="table table-bordered border-secondary">
                    <thead>
                        <tr>
                            <td className="text-center align-middle">
                                <strong>
                                    Option A
                                </strong>
                            </td>
                            <td className="text-center align-middle">
                            </td>
                            <td className="text-center align-middle">
                                <strong>
                                    Option B
                                </strong>
                            </td>
                        </tr>
                    </thead >
                    <tbody>
                        <tr>
                            <td className="text-center align-middle" rowspan={this.state.listItems.length + 1}>
                                With probability <strong>{this.props.prob_up}%</strong>: Get <strong>${this.props.pay_up}</strong>
                                <br></br>
                                    With probability <strong>{prob_down}%</strong>: Get <strong>${this.props.pay_down}</strong>
                            </td>
                        </tr>
                        {rows}
                        <tr>
                            <td className="text-center align-middle" colspan="3"><span id="feedback">Please enter your preferences.</span></td>
                        </tr>
                    </tbody>
                </table >
            </div >
        )
    }
}