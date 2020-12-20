class Templates:
    @staticmethod
    def simple_react_class_component(name):
        return """import {{ Component }} from "react";
import React from "react";

export default class {0} extends Component {{
  render() {{
    return <div>{{this.props.children}}</div>;
  }}
}}
""".format(name)

    @staticmethod
    def react_class_component_with_props_and_state(name):
        return """import {{ Component, HTMLAttributes }} from "react";
import React from "react";

interface Props extends HTMLAttributes<HTMLElement> {{}}

interface State {{}}

export default class {0} extends Component<Props, State> {{
  constructor(props: Props) {{
    super(props);
    this.state = {{}};
  }}

  render() {{
    return <div>{{this.props.children}}</div>;
  }}
}}
""".format(name)
