import React, {
  useEffect,
  useState
} from "react";

import {
  Container,
  Row,
  Col,
  Card,
  CardBody
} from "reactstrap";

import easyColor from "assets/img/badges/easy_color.png";
import easyGray from "assets/img/badges/easy_gray.png";

import hardColor from "assets/img/badges/hard_color.png";
import hardGray from "assets/img/badges/hard_gray.png";

import rainColor from "assets/img/badges/rain_color.png";
import rainGray from "assets/img/badges/rain_gray.png";

import morningColor from "assets/img/badges/morning_color.png";
import morningGray from "assets/img/badges/morning_gray.png";

import strongColor from "assets/img/badges/strong_color.png";
import strongGray from "assets/img/badges/strong_gray.png";

export default function Badge() {

const [badgeData, setBadgeData] =
  useState(null);

useEffect(() => {

  fetch("http://127.0.0.1:8000/badge")

    .then((response) =>
      response.json()
    )

    .then((data) => {
      setBadgeData(data);
    });

}, []);

  return (

    <main>
      <section
        className="section section-lg"
        style={{
          backgroundColor: "#172B4D",
          minHeight: "100vh"
        }}
      >
        <Container>
          <Row className="justify-content-center">
            <Col lg="10">
              <Card className="shadow border-0">
                <CardBody className="p-5">
                  <h2 className="mb-4">
                    🏆 포인트 / 뱃지
                  </h2>
                  <h4>
                    총 포인트: {badgeData?.total_points || 0}P
                  </h4>
                  <h5 className="mt-4">
                    획득 뱃지: {badgeData?.badge_count || 0} / 5
                  </h5>
                  <Row className="mt-5 justify-content-center">
                    <Col md="4" className="text-center mb-4">
                      <p className="mt-2 text-muted">
                        {badgeData?.easy_success_count || 0} / 30
                      </p>
                      <img
                        src={
                          badgeData?.badge_list?.includes("여유로운 통학의 신")
                          ? easyColor
                          : easyGray
                        }
                        alt=""
                        style={{
                            width: "180px",
                            height: "180px",
                            objectFit: "contain"
                        }}
                      />
                    </Col>
                    <Col md="4" className="text-center mb-4">
                      <p className="mt-2 text-muted">
                        {badgeData?.hard_success_count || 0} / 10
                      </p>
                      <img
                        src={
                          badgeData?.badge_list?.includes("아슬아슬 마스터")
                          ? hardColor
                          : hardGray
                        }
                        alt=""
                        style={{
                            width: "180px",
                            height: "180px",
                            objectFit: "contain"
                        }}
                      />
                    </Col>
                </Row>
                    <Row className="justify-content-center">
                    <Col md="4" className="text-center mb-4">
                      <p className="mt-2 text-muted">
                        {badgeData?.rain_success_count || 0} / 10
                      </p>
                      <img
                        src={
                          badgeData?.badge_list?.includes("비를 뚫는 자")
                          ? rainColor
                          : rainGray
                        }
                        alt=""
                        style={{
                            width: "180px",
                            height: "180px",
                            objectFit: "contain"
                        }}
                      />
                    </Col>
                    <Col md="4" className="text-center mb-4">
                      <p className="mt-2 text-muted">
                        {badgeData?.early_morning_count || 0} / 20
                      </p>
                      <img
                        src={
                          badgeData?.badge_list?.includes("새벽 통학생")
                          ? morningColor
                          : morningGray
                        }
                        alt=""
                        style={{
                            width: "180px",
                            height: "180px",
                            objectFit: "contain"
                        }}
                      />
                    </Col>
                    <Col md="4" className="text-center mb-4">
                      <p className="mt-2 text-muted">
                        {badgeData?.long_distance_count || 0} / 20
                      </p>
                      <img
                        src={
                          badgeData?.badge_list?.includes("강철 체력")
                          ? strongColor
                          : strongGray
                        }
                        alt=""
                        style={{
                            width: "180px",
                            height: "180px",
                            objectFit: "contain"
                        }}
                      />
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>
          </Row>
          <Card className="mt-5 shadow border-0">
            <CardBody>
              <Row>
                {/* 왼쪽 */}
                <Col md="6">
                  <h3 className="mb-4">
                  📖 포인트 도감
                  </h3>
                  <ul>
                    <li>
                      <strong>
                        여유로운 통학 성공
                      </strong>
                      <br />
                      지각 확률 20% 이하 통학 성공
                      (+10P)
                    </li>
                    <br />
                    <li>
                      <strong>
                        아슬아슬 통학 성공
                      </strong>
                      <br />
                      지각 확률 50% 이상 통학 성공
                      (+30P)
                   </li>
                    <br />
                   <li>
                      <strong>
                        험난한 날씨 속 통학 성공
                      </strong>
                     <br />
                      비 / 눈 오는 날 통학 성공
                      (+10P)
                   </li>
                    <br />
                    <li>
                     <strong>
                       혼잡 시간 통학 성공
                     </strong>
                     <br />
                     출퇴근 시간 통학 성공
                     (+10P)
                   </li>
                  </ul>
                </Col>

                {/* 오른쪽 */}
                <Col md="6">
                 <h3 className="mb-4">
                  📖 뱃지 도감
                  </h3>
                  <ul>
                    <li>
                      <strong>
                        여유로운 통학의 신
                      </strong>
                      <br />
                      지각 확률 20% 이하 30회 성공
                    </li>
                    <br />
                    <li>
                      <strong>
                       아슬아슬 마스터
                      </strong>
                      <br />
                      지각 확률 50% 이상 10회 성공
                    </li>
                    <br />
                    <li>
                      <strong>
                        비를 뚫는 자
                      </strong>
                      <br />
                      비 / 눈 오는 날 10회 성공
                    </li>
                    <br />
                    <li>
                      <strong>
                        새벽 통학생
                      </strong>
                      <br />
                      오전 7시 이전 통학 20회 성공
                    </li>
                    <br />
                    <li>
                      <strong>
                        강철 체력
                      </strong>
                      <br />
                      편도 1시간 이상 통학 20회 성공
                    </li>
                  </ul>
                </Col>
              </Row>
            </CardBody>
          </Card>
        </Container>
      </section>
    </main>
  );
}