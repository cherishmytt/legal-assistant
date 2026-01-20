# -*- coding: utf-8 -*-
"""
法律知识库更新脚本
运行此脚本将创建/更新完整的法律知识库
"""
import json
import os


def create_knowledge_base():
    """创建完整的法律知识库"""
    
    knowledge_base = {
        "labor_law": {
            "name": "劳动法律",
            "cases": [
                {
                    "title": "拖欠工资",
                    "keywords": ["工资", "拖欠", "欠薪"],
                    "laws": [
                        {
                            "name": "《中华人民共和国劳动法》",
                            "articles": [
                                {"number": "第五十条", "content": "工资应当以货币形式按月支付给劳动者本人。不得克扣或者无故拖欠劳动者的工资。"},
                                {"number": "第九十一条", "content": "用人单位有下列侵害劳动者合法权益情形之一的，由劳动行政部门责令支付劳动者的工资报酬、经济补偿，并可以责令支付赔偿金：（一）克扣或者无故拖欠劳动者工资的。"}
                            ]
                        },
                        {
                            "name": "《中华人民共和国劳动合同法》",
                            "articles": [
                                {"number": "第三十条", "content": "用人单位应当按照劳动合同约定和国家规定，向劳动者及时足额支付劳动报酬。"},
                                {"number": "第八十五条", "content": "用人单位拖欠或者未足额支付劳动报酬的，劳动者可以依法向当地人民法院申请支付令。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 与用人单位协商", "2. 向劳动监察部门投诉", "3. 申请劳动仲裁", "4. 向法院起诉"]
                },
                {
                    "title": "加班费",
                    "keywords": ["加班", "加班费", "超时工作"],
                    "laws": [
                        {
                            "name": "《中华人民共和国劳动法》",
                            "articles": [
                                {"number": "第四十四条", "content": "安排劳动者延长工作时间的，支付不低于工资的150%的报酬；休息日工作又不能补休的，支付不低于工资的200%的报酬；法定休假日工作的，支付不低于工资的300%的报酬。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 保留加班证据", "2. 与单位协商", "3. 申请劳动仲裁"]
                },
                {
                    "title": "违法解除劳动合同",
                    "keywords": ["辞退", "解雇", "裁员", "违法解除"],
                    "laws": [
                        {
                            "name": "《中华人民共和国劳动合同法》",
                            "articles": [
                                {"number": "第四十七条", "content": "经济补偿按劳动者在本单位工作的年限，每满一年支付一个月工资的标准向劳动者支付。"},
                                {"number": "第八十七条", "content": "用人单位违法解除劳动合同的，应当按经济补偿标准的二倍支付赔偿金。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 保留解除通知", "2. 申请劳动仲裁", "3. 要求继续履行或支付赔偿金"]
                },
                {
                    "title": "社会保险",
                    "keywords": ["社保", "五险一金", "养老保险", "医疗保险"],
                    "laws": [
                        {
                            "name": "《中华人民共和国社会保险法》",
                            "articles": [
                                {"number": "第五十八条", "content": "用人单位应当自用工之日起三十日内为其职工办理社会保险登记。"},
                                {"number": "第八十六条", "content": "用人单位未按时足额缴纳社会保险费的，由社保征收机构责令限期缴纳或补足。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 向社保部门投诉", "2. 申请劳动仲裁要求补缴"]
                }
            ]
        },
        "marriage_law": {
            "name": "婚姻家庭法律",
            "cases": [
                {
                    "title": "离婚财产分割",
                    "keywords": ["离婚", "财产分割", "夫妻共同财产"],
                    "laws": [
                        {
                            "name": "《中华人民共和国民法典》",
                            "articles": [
                                {"number": "第一千零六十二条", "content": "夫妻在婚姻关系存续期间所得的工资、奖金、投资收益等为夫妻共同财产。"},
                                {"number": "第一千零八十七条", "content": "离婚时，夫妻的共同财产由双方协议处理；协议不成的，由人民法院根据财产的具体情况判决。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 协议离婚到民政局办理", "2. 诉讼离婚向法院起诉", "3. 准备财产清单"]
                },
                {
                    "title": "子女抚养",
                    "keywords": ["抚养权", "抚养费", "子女", "监护"],
                    "laws": [
                        {
                            "name": "《中华人民共和国民法典》",
                            "articles": [
                                {"number": "第一千零八十四条", "content": "父母与子女间的关系，不因父母离婚而消除。"},
                                {"number": "第一千零八十五条", "content": "离婚后，一方抚养子女的，另一方应当负担部分或全部抚养费。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 协商确定抚养权", "2. 协商不成向法院起诉"]
                },
                {
                    "title": "家庭暴力",
                    "keywords": ["家暴", "家庭暴力", "人身保护令"],
                    "laws": [
                        {
                            "name": "《中华人民共和国反家庭暴力法》",
                            "articles": [
                                {"number": "第二条", "content": "家庭暴力是指家庭成员之间以殴打、捆绑、残害、限制人身自由以及经常性谩骂、恐吓等方式实施的侵害行为。"},
                                {"number": "第二十三条", "content": "当事人因遭受家庭暴力可以向人民法院申请人身安全保护令。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 及时报警", "2. 就医保留证据", "3. 申请人身保护令", "4. 起诉离婚"]
                }
            ]
        },
        "contract_law": {
            "name": "合同法律",
            "cases": [
                {
                    "title": "合同违约",
                    "keywords": ["违约", "合同", "违约金", "赔偿"],
                    "laws": [
                        {
                            "name": "《中华人民共和国民法典》",
                            "articles": [
                                {"number": "第五百七十七条", "content": "当事人一方不履行合同义务的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。"},
                                {"number": "第五百八十五条", "content": "当事人可以约定违约金。约定的违约金过分高于损失的，可以请求适当减少。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 保留合同和证据", "2. 发送违约通知", "3. 协商或仲裁/诉讼"]
                },
                {
                    "title": "借款合同",
                    "keywords": ["借款", "欠款", "债务", "利息"],
                    "laws": [
                        {
                            "name": "《中华人民共和国民法典》",
                            "articles": [
                                {"number": "第六百七十五条", "content": "借款人应当按照约定的期限返还借款。"},
                                {"number": "第六百八十条", "content": "禁止高利放贷，借款的利率不得违反国家有关规定。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 保留借款凭证", "2. 催告还款", "3. 向法院起诉"]
                }
            ]
        },
        "traffic_law": {
            "name": "交通事故法律",
            "cases": [
                {
                    "title": "交通事故赔偿",
                    "keywords": ["交通事故", "车祸", "赔偿", "保险"],
                    "laws": [
                        {
                            "name": "《中华人民共和国道路交通安全法》",
                            "articles": [
                                {"number": "第七十六条", "content": "机动车发生交通事故造成损害的，由保险公司在交强险限额内赔偿；不足部分按过错比例分担。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 报警保护现场", "2. 等待事故认定书", "3. 就医保留凭证", "4. 协商理赔或起诉"]
                }
            ]
        },
        "property_law": {
            "name": "房产法律",
            "cases": [
                {
                    "title": "房屋买卖",
                    "keywords": ["房产", "买卖", "过户", "产权"],
                    "laws": [
                        {
                            "name": "《中华人民共和国民法典》",
                            "articles": [
                                {"number": "第二百零九条", "content": "不动产物权的设立、变更、转让和消灭，经依法登记，发生效力。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 签订买卖合同", "2. 网签备案", "3. 缴纳税费", "4. 办理过户"]
                },
                {
                    "title": "房屋租赁",
                    "keywords": ["租赁", "租房", "房东", "租客"],
                    "laws": [
                        {
                            "name": "《中华人民共和国民法典》",
                            "articles": [
                                {"number": "第七百零三条", "content": "租赁合同是出租人将租赁物交付承租人使用、收益，承租人支付租金的合同。"},
                                {"number": "第七百二十二条", "content": "承租人无正当理由未支付租金的，出租人可以解除合同。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 签订租赁合同", "2. 办理备案", "3. 纠纷先协商", "4. 协商不成起诉"]
                }
            ]
        },
        "tort_law": {
            "name": "侵权责任法律",
            "cases": [
                {
                    "title": "人身损害赔偿",
                    "keywords": ["人身损害", "伤害", "赔偿", "医疗费"],
                    "laws": [
                        {
                            "name": "《中华人民共和国民法典》",
                            "articles": [
                                {"number": "第一千一百七十九条", "content": "侵害他人造成人身损害的，应当赔偿医疗费、护理费、交通费、营养费等合理费用。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 就医保留证据", "2. 报警", "3. 协商赔偿", "4. 起诉"]
                },
                {
                    "title": "名誉侵权",
                    "keywords": ["名誉", "诽谤", "侮辱", "隐私"],
                    "laws": [
                        {
                            "name": "《中华人民共和国民法典》",
                            "articles": [
                                {"number": "第一千零二十四条", "content": "民事主体享有名誉权。任何组织或者个人不得以侮辱、诽谤等方式侵害他人的名誉权。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 保留侵权证据", "2. 要求停止侵害", "3. 起诉要求赔偿"]
                }
            ]
        },
        "consumer_law": {
            "name": "消费者权益保护法律",
            "cases": [
                {
                    "title": "产品质量问题",
                    "keywords": ["质量", "退货", "三包", "消费者"],
                    "laws": [
                        {
                            "name": "《中华人民共和国消费者权益保护法》",
                            "articles": [
                                {"number": "第二十四条", "content": "经营者提供的商品不符合质量要求的，消费者可以退货或要求更换、修理。"},
                                {"number": "第五十五条", "content": "经营者有欺诈行为的，应当按照消费者的要求增加赔偿，增加赔偿的金额为价款的三倍，不足五百元的为五百元。"}
                            ]
                        }
                    ],
                    "procedures": ["1. 保留购物凭证", "2. 与商家协商", "3. 向消协投诉", "4. 起诉"]
                }
            ]
        }
    }
    
    return knowledge_base


def main():
    """主函数"""
    print("="*60)
    print("法律知识库更新工具")
    print("="*60)
    
    # 创建知识库
    print("\n正在创建法律知识库...")
    knowledge_base = create_knowledge_base()
    
    # 确保data目录存在
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"✓ 创建目录: {data_dir}")
    
    # 保存到文件
    file_path = os.path.join(data_dir, "knowledge_base.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 法律知识库已保存: {file_path}")
    
    # 统计信息
    total_cases = sum(len(category["cases"]) for category in knowledge_base.values())
    total_laws = 0
    for category in knowledge_base.values():
        for case in category["cases"]:
            total_laws += len(case["laws"])
    
    print(f"\n统计信息:")
    print(f"  - 法律分类: {len(knowledge_base)} 个")
    print(f"  - 案例类型: {total_cases} 个")
    print(f"  - 法律法规: {total_laws} 部")
    
    # 显示各分类详情
    print(f"\n分类详情:")
    for key, category in knowledge_base.items():
        case_count = len(category["cases"])
        print(f"  - {category['name']}: {case_count} 个案例")
    
    print("\n" + "="*60)
    print("✓ 更新完成！")
    print("="*60)


if __name__ == "__main__":
    main()
