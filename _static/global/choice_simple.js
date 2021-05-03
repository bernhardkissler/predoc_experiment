class ChoiceSimple extends React.Component {
    render() {
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
                                <strong>
                                    Option B
                                </strong>
                            </td>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td className="text-center align-middle">
                                With probability <strong>{this.props.prob_up}%</strong>: Get <strong>${this.props.pay_up}</strong>
                                <br></br>
                                    With probability <strong>{this.props.prob_down}%</strong>: Get <strong>${this.props.pay_down}</strong>
                            </td>
                            <td className="text-center align-middle">
                                Get <strong>${this.props.pay_certain}</strong> for certain (100%)
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        )
    }
}