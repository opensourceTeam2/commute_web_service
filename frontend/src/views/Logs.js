/*!

=========================================================
* Argon Design System React - v1.1.2
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-design-system-react
* Copyright 2023 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-design-system-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";

import {
  Card,
  CardBody,
  Container,
  Row,
  Col,
  Table,
} from "reactstrap";

import DemoNavbar from "components/Navbars/DemoNavbar.js";
import CardsFooter from "components/Footers/CardsFooter.js";

class Logs extends React.Component {

  state = {
    logs: []
  };

  componentDidMount() {

    document.documentElement.scrollTop = 0;
    document.scrollingElement.scrollTop = 0;
    this.refs.main.scrollTop = 0;

    const loginId =
      localStorage.getItem("loginId") || "guest";

    fetch(
      `http://127.0.0.1:8000/logs?login_id=${loginId}`
    )
      .then((response) =>
        response.json()
      )
      .then((data) => {
        this.setState({
          logs: data
        });
      });
  }

  render() {
    const logs = this.state.logs;

    return (
      <>
        <DemoNavbar />

        <main ref="main">
          <section className="section section-shaped section-lg">
            <div className="shape shape-style-1 bg-gradient-default">
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
              <span />
            </div>

            <Container className="pt-lg-7">
              <Row className="justify-content-center">
                <Col lg="10">
                  <Card className="shadow border-0">
                    <CardBody>
                      <h3 className="font-weight-bold">로그</h3>
                      <p className="text-muted">
                        로그인한 사용자가 지금까지 조회한 통학 도우미 결과를
                        요약해서 보여줍니다.
                      </p>

                      {logs.length === 0 ? (
                        <p className="mt-4">
                          아직 조회한 통학 도우미 결과가 없습니다.
                        </p>
                      ) : (
                        <Table responsive hover className="mt-4">
                          <thead>
                            <tr>
                              <th>조회 시간</th>
                              <th>출발 위치</th>
                              <th>수업 시작 시간</th>
                              <th>추천 1순위 경로</th>
                              <th>예상 소요 시간</th>
                              <th>지각 확률</th>
                            </tr>
                          </thead>
                          <tbody>
                            {logs.map((log, index) => {

                              return (
                                <tr key={index}>
                                  <td>{log.checkedAt}</td>
                                  <td>{log.startLocation}</td>
                                  <td>{log.classStartTime}</td>
                                  <td>{log.routeSummary}</td>
                                  <td>{log.totalMinutes}분</td>
                                  <td>{log.lateProbability}%</td>
                                </tr>
                              );
                            })}
                          </tbody>

                        </Table>
                      )}
                    </CardBody>
                  </Card>
                </Col>
              </Row>
            </Container>
          </section>
        </main>

        <CardsFooter />
      </>
    );
  }
}

export default Logs;