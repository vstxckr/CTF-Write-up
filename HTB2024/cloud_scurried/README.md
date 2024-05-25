# SCURRIED

> Cate: Cloud

# Description

Challenge cho chúng ta một file tên là [scurried.txt](/HTB2024/cloud_scurried/files/scurried.txt) nội dung file gồm một dòng chứa một chuỗi `AROAXYAFLIG2BLQFIIP34`

# Find Clues

Khi ta quăng chuỗi này lên google thì sẽ không nhận được kết quả gì có giá trị cả.

Tuy nhiên nếu để ý thì 4 ký tự đầu `AROA` khá có ý nghĩa, vì vậy ta sẽ tìm google với ký tự này cùng từ khoá `cloud id`.

Ta nhận được một url khá hữu ích về cách thức khai thác [`Derive a Principal ARN from an AWS Unique Identifier`](https://hackingthe.cloud/aws/enumeration/enumerate_principal_arn_from_unique_id/)

Tìm kiếm thông tin về mô tả trên, ta kiếm được một blog nói một cách khá chi tiết về cách thức thực hiện để có thể lấy ARN từ một AWS ID [blog](https://awsteele.com/blog/2023/11/19/reversing-aws-iam-unique-ids.html)

# Capture the flag

Thực hiện thêm CloudTrail bucket policy theo hướng dẫn của AWS [link](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-s3-bucket-policy-for-cloudtrail.html)

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Principal": {
        "AWS": "AROAXYAFLIG2BLQFIIP34"
      },
      "Effect": "Deny",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::aunau/*"
    }
  ]
}
```

Sau khi đã thêm ta mở lại bucket policy, khi đó AWS ID đã trở thành ARN, lấy nguyên chuỗi này và cho vào flag form `HTB{}` là ta có flag.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Principal": {
                "AWS": "arn:aws:iam::532587168180:role/vault101"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::aunau/*"
        }
    ]
}
```

# Flag

`HTB{arn:aws:iam::532587168180:role/vault101}`