import React, { Component } from 'react';
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem } from 'reactstrap';

let config = require('../config.json');

export default class NavbarComponent extends Component {

  constructor()
  {
    super();
    this.state = {};
  }
  render() {
    return (
      <div className="navbarcomponent">
        <div>
        <Navbar color="light" light expand="md">
          <NavbarBrand href="/">spotifun</NavbarBrand>
          <NavbarToggler onClick={this.toggle} />
          <Collapse isOpen={this.state.isOpen} navbar>
            <Nav className="ml-auto" navbar>
              <NavItem>
                <NavLink href={config.frontend_hostname + ""}>Login</NavLink>
              </NavItem>
              <NavItem>
                <NavLink href={config.frontend_hostname + "home"}>Home</NavLink>
              </NavItem>
              <NavItem>
                <NavLink href={config.frontend_hostname + "playlist_creator"}>Playlist Creator</NavLink>
              </NavItem>
              {/* <UncontrolledDropdown nav inNavbar>
                <DropdownToggle nav caret>
                  Options
                </DropdownToggle>
                <DropdownMenu right>
                  <DropdownItem>
                    Option 1
                  </DropdownItem>
                  <DropdownItem>
                    Option 2
                  </DropdownItem>
                  <DropdownItem divider />
                  <DropdownItem>
                    Reset
                  </DropdownItem>
                </DropdownMenu>
              </UncontrolledDropdown> */}
            </Nav>
          </Collapse>
        </Navbar>
      </div>
      </div>
    )
  }
}
