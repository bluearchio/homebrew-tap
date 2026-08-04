class BluearchAwsTags < Formula
  desc "AWS tagging, lifecycle, tag policy, and FinOps CLI"
  homepage "https://github.com/bluearchio/bluearch-aws-tags"
  url "https://github.com/bluearchio/bluearch-aws-tags/releases/download/v0.12.7/bluearch-aws-tags-macos-arm64.zip"
  version "0.12.7"
  sha256 "1ea8b8940e63e22068515db878bc7d86c670cc1703cfd96a3304c17f56b4e9c7"
  license "MIT"

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "bluearch-aws-tags"
  end

  def caveats
    <<~EOS
      bluearch-aws-tags has been installed.

      Start Core first:
        bluearch-aws-core start --daemon

      Commands:
        bluearch-aws-tags --help

      Getting started:
        bluearch-aws-tags setup validate

      Configure AWS credentials:
        export AWS_PROFILE=your-profile
        aws sso login

      Data is stored locally by the product runtime.
    EOS
  end

  test do
    system "#{bin}/bluearch-aws-tags", "--version"
  end
end
